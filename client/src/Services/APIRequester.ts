import axios from 'axios';

export const getPoints = async (hour:number,setResponse:Function) => {
    axios.get(`http://localhost:5000/api/gridload?time=${hour}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        },
    }).then(response => setResponse(response.data));
};