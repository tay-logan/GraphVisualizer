import pandas as pd
import numpy as np
import glob
from LocalDataHandler import *
from dateutil import tz
import uuid
from datetime import timedelta, datetime

def prepareFeature(df, feature, time_inter, timeSetting):
    # Prepares the features for a graph, with fi
    time_type = 'Datetime (Local)' if timeSetting == "Local" else 'Datetime (UTC)'

    # Limites the dataframe rows to the time interval and time bounds

    df = df.copy()
    df = df.iloc[::time_inter]
    
    if feature not in df.columns:
        raise ValueError(f"{feature} not found in dataframe columns")

    # Returns the time values and the feature values from the dataframe
    time_values = df[time_type]
    feature_values = df[feature]

    return time_values, feature_values

class _FeatureData:
    """Used to hold the information from a summary.csv file"""
    def __init__(self, filePath: str) -> None:
        # Saves the basic file path, participant, and dataframe
        self.filePath = filePath
        self.participantID = filePath.split("/")[-2]
        self.df = pd.read_csv(filePath, parse_dates=['Datetime (UTC)'],
                              date_parser=lambda x: pd.to_datetime(x, format='%Y-%m-%dT%H:%M:%SZ'))    
        
        self.df["On Wrist"] =self.df["On Wrist"].astype(bool)      
        
        # Creates a new dataframe column with the local timezone
        timeOffset = int(self.df["Timezone (minutes)"][0]) * 60
        self.df['Datetime (Local)'] = self.df['Datetime (UTC)'] + timedelta(seconds=timeOffset)
        
        # Removes the Unix Timestamp, and Timezone
        self.df.drop("Unix Timestamp (UTC)", axis=1, inplace=True)
        self.df.drop("Timezone (minutes)", axis=1, inplace=True)
                
    def addData(self, newDF):
        oldDF = self.df
        oldTime = oldDF["Datetime (UTC)"]
        
        newDF = newDF[~newDF["Datetime (UTC)"].isin(oldTime)]
        
        self.df = pd.concat([oldDF, newDF])
        self.df.sort_values(by=["Datetime (UTC)"], inplace=True)
        self.df.reset_index(drop=True, inplace=True)
        
class DataFilter:
    def __init__(self, feature: str, comparator: str, value: float | int | bool) -> None:
        self.filterID = str(uuid.uuid4())
        self.feature = feature
        self.comparator = comparator
        self.value = value
        
        self.chipDisplay = None
        
    def applyTo(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.comparator == "==":
            data.loc[data[self.feature] != self.value, :] = np.nan
            return data
        elif self.comparator == "!=":
            data.loc[data[self.feature] == self.value, :] = np.nan
            return data
        elif self.comparator == ">":
            data.loc[data[self.feature] <= self.value, :] = np.nan
            return data
        elif self.comparator == "<":
            data.loc[data[self.feature] >= self.value, :] = np.nan
            return data
        elif self.comparator == ">=":
            data.loc[data[self.feature] < self.value, :] = np.nan
            return data
        elif self.comparator == "<=":
            data.loc[data[self.feature] > self.value, :] = np.nan
            return data
        else :
            return ValueError("Comparator is not valid")
                
    def __str__(self) -> str:
        if self.feature == "On Wrist":
            if self.value if self.comparator == "==" else not self.value:
                return "On Wrist" 
                
            return "Off Wrist"
        
        return f"{self.feature} {self.comparator} {self.value}"
        
    def __eq__(self, __value: object) -> bool:
        self.filterID == __value.filterID
        
class DataHandler:
    """The brains that holds the functions that control the feature data"""
    def __init__(self, store) -> None:
        # The list of all files imported
        self.featureDataList = []
        
        # The list of all callbacks then data changes
        self.data_change_callbacks = []
        self.graphs = {}
        
        self.filters = []
        
        # store callback
        self.store = store
        
        self.timezone = readFile("settings", ["time"])
        
        self.lowerLimit = None
        self.upperLimit = None
        
        self.lowerRange = None
        self.upperRange = None
        
    def getFilesfromFolder(self, folder_path) -> list:
        """Gets a list of files found inside the folder, or inside folders recursively"""
        folder_path = folder_path + "/**/summary.csv"
        files = glob.glob(folder_path, recursive=True)
        
        return files
    
    def importFromFolder(self, folder_path) -> int:    
        """Import files from a folder path"""
        savedFiles = readFile("imports")  
        
        files = self.getFilesfromFolder(folder_path)
        
        # for each file it imports it, and appends to recent files
        for file in files:
            self.importFromFile(file) 
            
            if file not in savedFiles:
                savedFiles.append(file)
            
        saveFile("imports", [], savedFiles)
        
        return len(files)
    
    def importFromFile(self, file):
        """Imports a file from its path"""
        allParticipants = self.getParticipantsList()
        newFeatureData = _FeatureData(file.replace("\\", "/"))
        curParticipant = newFeatureData.participantID
        
        if curParticipant not in allParticipants:
            self.featureDataList.append(newFeatureData)   
        else:
            index = self.featureDataList.index(self.getParticipantData(curParticipant))
            self.featureDataList[index].addData(newFeatureData.df)
                    
        self.updateTimeLimits()

    def getParticipantData(self, participantID: int) -> list:
        """Returns the Featuredata for a certain participant"""
        try:
            return [data for data in self.featureDataList if data.participantID == participantID][0]
        except:
            return None
        
    def getAllData(self):
        """Returns all imported feature data"""
        return self.featureDataList

    def clearData(self):
        """Deletes all the imported feature data"""
        self.featureDataList = []
    
    def getParticipantsList(self) -> list:
        """Returns a list off all participants that have feature data"""
        return list(set([featureData.participantID for featureData in self.featureDataList]))
    
    def getColumnsList(self) -> list:
        """Returns a list of the columns found in the import feature data"""
        columns = []
        
        for featureData in self.featureDataList:
            columns += featureData.df.columns.to_list()
        
        return sorted(list(set(columns)), key=lambda column: columns.index(column))
    
    def getFeaturesList(self) -> list:
        """Returns the feature found in the feature data (exclude time columns)"""
        excludeList = ['Datetime (UTC)', 'Datetime (Local)']
        feartures = self.getColumnsList()
            
        filteredColumns = list(filter(lambda column: column not in excludeList, feartures))
        
        return filteredColumns

    def register_data_update_callback(self, callback):
        """adds a function to be called on data update"""
        self.data_change_callbacks.append(callback)

    def updateDataHandler(self):
        """Calls all update functions"""
        for callback in self.data_change_callbacks:
            callback()
            
    def getGraph(self, graphID: str) -> dict:
        """Returns the graph information for a given graph ID"""
        return self.graphs[graphID]
    
    def get_graphID(self, participantID: str, feature: str):
        """Returns a graph ID from a specified participant and feature"""
        for graphID, graph in self.graphs.items():
            if graph["data"].participantID == participantID and graph["y_var"] == feature:
                return graphID
        return None

    def add_graph(self, participantID: str, graph_t, y_var, inter, b_color, d_color) -> str:        
        """Adds a new graph to the list of graphs"""
        
        # Finds the relevant feature data for a participant
        featureData = self.getParticipantData(participantID)
        
        # Generates a unique graph ID
        newGraphId = str(uuid.uuid4())
        
        # Sets the relevant graph into into the dict
        self.graphs[newGraphId] = {
            "data": featureData,
            "graph_t": graph_t,
            "y_var": y_var,
            "inter": inter,
            "b_color": b_color,
            "d_color": d_color
        }
        
        return newGraphId

    def updateGraphVisuals(self, graphID: str, graph_t, inter, b_color, d_color) -> bool:
        """Update already existing graph options"""
        
        # Updates the existing graph dict
        if graphID in self.graphs:
            graph = self.graphs[graphID]
            
            graph["graph_t"] = graph_t
            graph["inter"] = inter
            graph["b_color"] = b_color
            graph["d_color"] = d_color
            
            return True
        else:
            print(f"Graph ID {graphID} not found.")
            return False
        
    def _updateGraphData(self, graphID: str) -> bool:
        """Update already existing graph options"""
        graph = self.getGraph(graphID)
        
        featureData = graph["data"]
        y_var = graph["y_var"]
        inter = graph["inter"]
        
        local_s = self.timezone
        s_time = self.lowerRange
        e_time = self.upperRange
        time_type = 'Datetime (Local)' if local_s == "Local" else 'Datetime (UTC)'
        
        df = featureData.df.copy().iloc[:, 1:-1]
        
        for filter in self.filters:
            df = filter.applyTo(df)       
            
        df = pd.concat([featureData.df.iloc[:, 0], df, featureData.df.iloc[:, -1]], axis=1)
        df = df[df[time_type] >= s_time]
        df = df[df[time_type] <= e_time]
        # Genetates new time and feature values
        time_values, feature_values = prepareFeature(df, y_var, inter, local_s)
        
        # Updates the existing graph dict
        graph["time_values"] = time_values
        graph["feature_values"] = feature_values
        graph["inter"] = inter
        graph["local_time"] = local_s
        
        # Update the displayed graph
        if "graph_fig" in graph.keys():
            graph["graph_fig"].updateGraph()
        else :
            self.store.displayGraph(graphID)
        
        return True


    def delete_graph(self, graphID: str) -> None:
        """Delete certain graph and graph figure"""
        
        # Get the graphs for the selected participant
        rowIndex = list(self.graphs.keys()).index(graphID)
        self.store.delete_graph(rowIndex)
        
        # Delete Graph from list
        del self.graphs[graphID]

        # Update universal app callback
        self.store.dataHandler.updateDataHandler()
           
    def deleteAllGraphs(self) -> None:
        """Delete all graphs and visuals"""
        
        # Delete all rows from the body
        graphCount = len(self.graphs)
        self.store.deleteAllGraphs(graphCount)
        
        # Clear the graphs
        self.graphs = {}

        # Update universal app callback
        self.store.dataHandler.updateDataHandler()  

    def getGraphIDTime(self, graphID: str) -> list:
        """Returns the time column from a graph"""
        graphDict = self.getGraph(graphID)
        return graphDict["time_values"]    
    
    def addFilter(self, feature: str, comparator: str, value: float | bool) -> DataFilter:
        newFilter = DataFilter(feature, comparator, value)
        self.filters.append(newFilter)
        self.store.dataHandler.updateDataHandler()
        self.updateAllGraphs()
        
    def getFilterForFeature(self, feature: str) -> list:
        return [filter for filter in self.filters if filter.feature == feature]
    
    def findFilter(self, filterID: str) -> list:
        return [filter for filter in self.filters if filter.filterID == filterID]
    
    def getAllFilters(self) -> list:
        return self.filters
    
    def deleteFilter(self, filterID: str) -> None:
        index = [filter.filterID for filter in self.filters].index(filterID)
        del self.filters[index]
        self.store.dataHandler.updateDataHandler()
        self.updateAllGraphs()
        
    def deleteAllFilters(self) -> None:
        for _ in range(len(self.filters)):
            self.filters[0].chipDisplay.close()
            
        self.filters = []
        
    def updateAllGraphs(self):
        for graphID in self.graphs.keys():
            self._updateGraphData(graphID)
        
    def changeTimezone(self, timezone) -> None:
        self.timezone = timezone
        curtimeCol = "Datetime (Local)" if self.timezone == "Local" else "Datetime (UTC)"
        oldTimeCol = "Datetime (Local)" if not self.timezone == "Local" else "Datetime (UTC)"
        
        if self.upperLimit is not None and self.upperLimit is not None:
            data = self.getAllData()[0].df
            
            self.lowerLimit = data[data[oldTimeCol] == self.lowerLimit][curtimeCol].iloc[0]
            self.upperLimit = data[data[oldTimeCol] == self.upperLimit][curtimeCol].iloc[0]
        
            if self.lowerRange is not None and self.upperRange is not None:
                self.lowerRange = data[data[oldTimeCol] == self.lowerRange][curtimeCol].iloc[0]
                self.upperRange = data[data[oldTimeCol] == self.upperRange][curtimeCol].iloc[0]
        
        self.updateAllGraphs()
        self.updateDataHandler()

    def updateTimeLimits(self):
        timeColumn = "Datetime (Local)" if self.timezone == "Local" else "Datetime (UTC)"
        
        firstDF = self.featureDataList[0].df
        lowerLimit = firstDF.loc[0, timeColumn]
        upperLimit = firstDF.loc[len(firstDF)-1, timeColumn]

        for data in self.featureDataList:
            firstTime = data.df.loc[0, timeColumn]
            lastTime = data.df.loc[len(data.df)-1, timeColumn]
            
            if firstTime > lowerLimit:
                lowerLimit = firstTime
            
            if lastTime < upperLimit:
                upperLimit = lastTime
              
        self.lowerLimit = lowerLimit
        self.upperLimit = upperLimit
        
        updateGraphs = False
        if self.lowerRange is None or self.lowerRange < lowerLimit:
            self.lowerRange = lowerLimit
            updateGraphs = True
            
        if self.upperRange is None or self.upperRange > upperLimit:
            self.upperRange = upperLimit
            updateGraphs = True
            
        if updateGraphs:
            self.updateAllGraphs()
            
    def setTimeRanges(self, lowerRange, upperRange):
        self.lowerRange = datetime.strptime(lowerRange, '%Y-%m-%d %H:%M:%S')
        self.upperRange = datetime.strptime(upperRange, '%Y-%m-%d %H:%M:%S')
        
        self.updateAllGraphs()
        
    def getTimeRanges(self) -> list [datetime, datetime]:
        return self.lowerRange, self.upperRange
        
    def getTimeValues(self):
        data = self.getAllData()[0].df
        timeName = "Datetime (Local)" if self.timezone == "Local" else "Datetime (UTC)"
        timeSeries = data[timeName]
        
        timeSeries = timeSeries[timeSeries >= self.lowerLimit]
        timeSeries = timeSeries[timeSeries <= self.upperLimit]
        
        return timeSeries.to_list()