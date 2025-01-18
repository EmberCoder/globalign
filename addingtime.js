
async function fetchData() {
    try {
      const response = await fetch('https://api.example.com/data'); 
  
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
  