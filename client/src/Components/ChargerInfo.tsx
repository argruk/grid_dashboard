// @flow
import * as React from 'react';
import {ChargerData} from "./Dashboard";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";

interface OwnProps {
    chargers: Array<ChargerData>,
}

export const ChargerInfo = ({chargers}: OwnProps) => {
    return (
        <div style={{overflow:"auto", height:'60vh'}}>
            {
                chargers.map((charger) =>
                    <Card style={{margin:'5px'}} key={charger.cadaster}>
                        <CardActionArea>
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="h2">
                                    <b> Charger: </b>{charger.cadaster}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    <b> Address: </b> {charger.address}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    <b> Predicted car model: </b> {charger.carModel}
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    <b> Predicted charge need: </b> {charger.chargeNeed} kW
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    <b> Optimized charge: </b> {charger.optimizedCharge} kW
                                </Typography>
                                <Typography variant="body2" color="textSecondary">
                                    <b> Decreased by: </b> {Math.ceil(charger.decreasePercent)} %
                                </Typography>
                            </CardContent>
                        </CardActionArea>
                    </Card>
                )
            }

        </div>
    );
};
