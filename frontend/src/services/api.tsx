import axios from "axios";
import { io } from 'socket.io-client';

const VIRTUAL_URL = "http://192.168.1.91:5000/api/"; 

const instance = axios.create({
    baseURL: VIRTUAL_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 5000,
});

export const socket = io(VIRTUAL_URL, {
    withCredentials: true,
});

export default instance;