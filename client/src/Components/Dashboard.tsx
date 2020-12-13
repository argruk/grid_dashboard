import React, {FunctionComponent, useEffect, useState} from 'react';
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
    cadaster: string
}

type Props = OwnProps;

const Dashboard: FunctionComponent<Props> = (props) => {
    const [dataPoints, setDataPoints] = useState<Array<Points>>([]);
    useEffect(()=>{
        getPoints(12,setDataPoints)
    },[]);

  return (
      <div>

      </div>
  );
};

export default Dashboard;

