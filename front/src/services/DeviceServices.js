class DeviceService {

    async getDevices(pi_name) {
        try {
            const response = await fetch('http://localhost:5000/api/get_devices/' + pi_name, {
                method: 'GET',
            });

            const data = await response.json();
            // console.log(data)
            if (data != null)
                return data;
            else 
                return 0;
        } 

        catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    }

    async getTopics(pi_name) {
        try {
            const response = await fetch('http://localhost:5000/api/get_topics/' + pi_name, {
                method: 'GET',
            });

            const data = await response.json();
            // console.log(data)
            if (data != null)
                return data;
            else 
                return 0;
        } 

        catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    }

    async turnOffAlarm(pin) {
        try {
            const response = await fetch('http://127.0.0.1:5000/turn-off-alarm/' + pin, {
                method: 'PUT',
            });
            const data = await response.json();
            // console.log(data)
            if (data != null)
                return data;
            else 
                return 0;
        } 

        catch (error) {
            console.error('Error fetching data:', error);
            throw error;
        }
    }
    
}  
export default new DeviceService();
