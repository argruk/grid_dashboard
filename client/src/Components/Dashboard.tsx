import React, {FunctionComponent, useEffect, useState} from 'react';
import PlotlyChart from 'react-plotlyjs-ts';
import {getPoints} from "../Services/APIRequester";


interface OwnProps {}

interface Points{
    lat:number,
    lon: number,
    time: string,
    predictedLoad: number,
    isOverloaded: boolean,
    baseLoad: number,
    maxLoad: number,
    cadaster: string,
    [key: string]: any
}

type Props = OwnProps;

const Dashboard: FunctionComponent<Props> = (props) => {
    const [dataPoints, setDataPoints] = useState<Array<Points>>([]);
    const [lat, setLat] = useState<Array<number>>([]);
    const [lon, setLon] = useState<Array<number>>([]);

    const getBy = (key:string) => {
        return dataPoints.map(point => {return point[key]})
    };

    const average = (nums:Array<number>) => {
        return nums.reduce((a, b) => (a + b),0) / nums.length;
    };

    useEffect(()=>{
        getPoints(12,setDataPoints)
    },[]);

    useEffect(()=>{
        setLat(getBy('lat'));
        setLon(getBy('lon'));
    },[dataPoints]);


  return (
      (lat && lon)?
          (<PlotlyChart
              data={[
                  {
                      type: "scattermapbox",
                      lon: lon,
                      lat: lat,
                      marker: { color: "red", size: 7 }
                  }
              ]}
              layout={
                  {
                      dragmode: "zoom",
                      mapbox: { style: "open-street-map", center: { lat: average(lat), lon: average(lon) }, zoom: 11 },
                      margin: { r: 0, t: 0, b: 0, l: 0 }
                  }
              }
              onClick={(event)=>{console.log(event.points)}}
              onHover={()=>{}}
          />)
          :
          (<></>)

  );
};

export default Dashboard;

