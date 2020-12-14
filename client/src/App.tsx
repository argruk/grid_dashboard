import React, {useState} from 'react';
import './App.css';
import Dashboard, {GridData} from "./Components/Dashboard";
import {GridInfo} from "./Components/GridInfo";
import {Grid} from "@material-ui/core";

function App() {

    const [selectedGrid, setSelectedGrid] = useState<GridData|undefined>(undefined);
    const [focused, setFocused] = useState<boolean>(false);

    return (
        <div className="App">
          <header className="App-header">
              <Grid container spacing={4}>
                  <Grid item xs={selectedGrid ? 9 : 12}>
                      <Dashboard setSelectedGrid={setSelectedGrid} focused={focused} setFocused={setFocused} selectedGrid={selectedGrid}/>
                  </Grid>
                  {selectedGrid &&
                      <Grid item xs={3}>
                          <GridInfo selectedGrid={selectedGrid} setSelectedGrid={setSelectedGrid} setFocused={setFocused}/>
                      </Grid>
                  }
              </Grid>
          </header>
        </div>
    );
}

export default App;

