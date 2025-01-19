

async function fetchData() {
    try {
      const response = await fetch('https://timeapi.io/api/conversion/converttimezone', {
        method: "POST",
        body: JSON.stringify(
          {
            "fromTimeZone": continentandcountry,
            "dateTime": "2021-03-14 17:45:00",
            "toTimeZone": "America/Los_Angeles",
            "dstAmbiguity": ""
          }
        ),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      }
      ); 
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      const data = await response.json();
      return data;
  
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  }
  
  // Example usage:
  fetchData()
    .then(data => console.log(data))
    .catch(error => console.error(error));
  