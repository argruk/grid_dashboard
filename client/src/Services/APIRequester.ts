import axios from 'axios';

export const getPoints = async (hour:number,setResponse:Function) => {
    axios.get(`http://localhost:5000/api/gridload?time=${hour}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => setResponse(response.data));
};

export const getChargers = async (time:number,cadaster:string,baseload:number,maxload:number,setChargers:Function) => {
    axios.get(`http://localhost:5000/api/charging?time=${time}&cadaster=${cadaster}&baseLoad=${baseload}&maxLoad=${maxload}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => setChargers(response.data));
};