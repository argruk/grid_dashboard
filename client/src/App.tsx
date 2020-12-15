import React, {useState} from 'react';
import './App.css';
import Dashboard, {GridData, ChargerData} from "./Components/Dashboard";
import {GridInfo} from "./Components/GridInfo";
import {Grid} from "@material-ui/core";
import {ChargerInfo} from "./Components/ChargerInfo";

function App() {

    const [selectedGrid, setSelectedGrid] = useState<GridData|undefined>(undefined);
    const [focused, setFocused] = useState<boolean>(false);
    const [chargers, setChargers] = useState<Array<ChargerData>>([]);

    return (
        <div className="App">
          <header className="App-header">
              <Grid container spacing={4}>
                  <Grid item xs={selectedGrid ? 9 : 12}>
                      <Dashboard
                          setSelectedGrid={setSelectedGrid}
                          focused={focused}
                          setFocused={setFocused}
                          selectedGrid={selectedGrid}
                          chargers={chargers}
                          setChargers={setChargers}
                      />
                  </Grid>
                  {selectedGrid &&
                      <Grid item xs={3}>
                          <GridInfo
                              selectedGrid={selectedGrid}
                              setSelectedGrid={setSelectedGrid}
                              setFocused={setFocused}
                          />
                          <ChargerInfo chargers={chargers}/>
                      </Grid>
                  }
              </Grid>
          </header>
        </div>
    );
}

export default App;

