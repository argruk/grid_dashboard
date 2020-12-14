import React, {ChangeEvent, FunctionComponent, useEffect, useState} from 'react';
import PlotlyChart from 'react-plotlyjs-ts';
import {getChargers, getPoints} from "../Services/APIRequester";
import Container from '@material-ui/core/Container';
import {NativeSelect, Typography} from "@material-ui/core";


interface OwnProps {}

interface Points{
    lat:number,
    lon: number,
    time: number,
    predictedLoad: number,
    isOverloaded: string,
    baseLoad: number,
    maxLoad: number,
    cadaster: string,
    [key: string]: any
}

interface Chargers {
    lon: number,
    lat: number,
    carModel: string,
    chargeNeed: number,
    optimizedCharge: number
}

const times:Array<number> = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24];

type Props = OwnProps;



const Dashboard: FunctionComponent<Props> = (props) => {
    const [time, setTime] = useState<number>(12);

    const [dataPoints, setDataPoints] = useState<Array<Points>>([]);
    const [lat, setLat] = useState<Array<number>>([]);
    const [lon, setLon] = useState<Array<number>>([]);
    const [colors, setColors] = useState<Array<string>>(['black']);
    const [centerPoint, setCenterPoint] = useState<Array<number>|undefined>(undefined);
    const [chargers, setChargers] = useState<Array<Chargers>>([]);


    const getBy = (dataset:Array<any>,key:string) => {
        return dataset.map(point => {return point[key]})
    };

    const getColors = () => {
        return dataPoints.map(point => {return (point['isOverloaded'] === "True")? ('red') : ('blue') })
    };

    const average = (nums:Array<number>) => {
        return nums.reduce((a, b) => (a + b),0) / nums.length;
    };

    const loadTime = (event:ChangeEvent<HTMLSelectElement>) => {
        setTime(+event.target.value);
        getPoints(+event.target.value,setDataPoints);
    };

    const handleOverloadedClick = (point:Points) => {
        getChargers(point.time,point.cadaster,point.baseLoad,point.maxLoad,setChargers);
    };

    useEffect(()=>{
        getPoints(time,setDataPoints)
    },[]);

    useEffect(()=>{
        let lat_a = getBy(dataPoints,'lat');
        let lon_a = getBy(dataPoints,'lon');
        let colors_a = getColors();

        setLat(lat_a);
        setLon(lon_a);
        setColors(colors_a);
        setCenterPoint([average(lat_a),average(lon_a)]);
    },[dataPoints]);

    // useEffect(()=>{setCenterPoint([average(getBy(chargers,'lon')),average(getBy(chargers,'lat'))])},[chargers]);

  return (
      (lat && lon && centerPoint)?
          (
              <Container>
                  <Typography variant={"h5"}>Please, select time of the day</Typography>
                  <NativeSelect
                      value={time}
                      style={{margin:"8vh",backgroundColor:"white",width:"8vw"}}
                      onChange={(event)=>{loadTime(event)}}
                      inputProps={{
                          name: 'time',
                          id: 'age-native-label-placeholder',
                      }}
                  >
                      {times.map( (t,idx) => {
                          return <option key={idx} value={t}>{t}</option>
                      })}
                  </NativeSelect>
                  <Container>
                      <PlotlyChart
                          data={[
                              {
                                  type: "scattermapbox",
                                  lon: lon,
                                  lat: lat,
                                  marker: { color: colors, size: 10 }
                              }
                          ]}
                          layout={
                              {
                                  dragmode: "zoom",
                                  mapbox: { style: "open-street-map", center: { lat: centerPoint[0], lon: centerPoint[1] }, zoom: 11 },
                                  margin: { r: 0, t: 0, b: 0, l: 0 }
                              }
                          }
                          onClick={(event)=>{handleOverloadedClick(dataPoints[event.points[0].pointIndex])}}
                          onHover={()=>{}}
                      />
                  </Container>

              </Container>
              )
          :
          (<></>)

  );
};

export default Dashboard;

