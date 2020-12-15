// @flow
import Typography from '@material-ui/core/Typography';
import * as React from 'react';
import {GridData} from "./Dashboard";
import {Button} from "@material-ui/core";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import CardActions from '@material-ui/core/CardActions';
import {Dispatch, SetStateAction} from "react";

interface OwnProps {
    selectedGrid: GridData
    setSelectedGrid: Function,
    setFocused:Dispatch<SetStateAction<boolean>>,
}

export const GridInfo = ({selectedGrid, setSelectedGrid,setFocused}: OwnProps) => {
    return (
        <Card style={{margin:'5px'}}>
            <CardActionArea>
                <CardContent>
                    <Typography gutterBottom variant="h5" component="h2">
                        <b> Grid: </b>{selectedGrid.cadaster}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        <b> Address: </b> {selectedGrid.address}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        <b> Base load: </b> {selectedGrid.baseLoad} kW
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        <b> Max load: </b> {selectedGrid.maxLoad} kW
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                        <b> Predicted load: </b> {selectedGrid.predictedLoad} kW
                    </Typography>
                </CardContent>
            </CardActionArea>
            <CardActions>
                <Button size="small" color="primary" onClick={()=>{setSelectedGrid(undefined);setFocused(false)}}>
                    Close
                </Button>
            </CardActions>
        </Card>
    );
};
