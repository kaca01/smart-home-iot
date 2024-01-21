import React from 'react';
import { Devices } from './components/Devices/Devices';

const AppRoutes = [
    {        
        path: "/devices",
        element: <Devices></Devices>
    },

    {
        path: '/',  // TODO: change this later
        element: <Devices></Devices>
      }
];

export default AppRoutes;