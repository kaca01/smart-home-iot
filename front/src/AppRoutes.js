import React from 'react';
import { Devices } from './components/Devices/Devices';
import { Grafana } from './components/Grafana/Grafana';

const AppRoutes = [
    {        
        path: "/devices",
        element: <Devices></Devices>
    },

    {
        path: '/',  // TODO: change this later
        element: <Devices></Devices>
    },

    {
        path: '/grafana',
        element: <Grafana></Grafana>
    }
];

export default AppRoutes;