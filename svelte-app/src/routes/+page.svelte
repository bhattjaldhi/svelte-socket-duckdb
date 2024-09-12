<script>
    import { onMount } from "svelte";
    import { Button } from "flowbite-svelte";
    import io from 'socket.io-client';
  
    let tableData = [];
    let socket;
  
    // Establish WebSocket connection
    onMount(() => {
      socket = io('http://ec2-54-226-66-45.compute-1.amazonaws.com');  // Connect to Flask SocketIO server
      fetchData();
  
      // Listen for update success message from the backend
      socket.on('update_success', (data) => {
        console.log(`Update successful for row: ${data.row_id}, column: ${data.column}`);
      });
  
      // Listen for broadcasted cell updates from other users
      socket.on('cell_update_broadcast', (data) => {
        const { row_id, column, new_value } = data;
        updateTableDataBroadcast(row_id, column, new_value);
      });
  
      // Handle errors
      socket.on('update_failure', (data) => {
        console.error('Error updating data:', data.error);
      });
    });
  
    // Fetch initial data from the Flask API
    const fetchData = async () => {
      try {
        const response = await fetch("http://ec2-54-226-66-45.compute-1.amazonaws.com/api/table");
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        tableData = await response.json();
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };
  
    // Send updated cell data to Flask via WebSocket
    const updateCell = (rowId, column, value) => {
      socket.emit('cell_update', { row_id: rowId, column: column, new_value: value });
    };
  
    // Update the tableData array locally when a cell update is received from another user
    const updateTableDataBroadcast = (rowId, column, newValue) => {
      const rowIndex = tableData.findIndex(row => row.id === rowId);
      if (rowIndex !== -1) {
        tableData[rowIndex][column] = newValue;
      }
    };
  
    // Update the tableData array and send the change to the server
    const updateTableData = (index, field, value) => {
      tableData[index][field] = value;
      updateCell(tableData[index].id, field, value);
    };
  </script>
  
  <div class="container mx-auto p-4">
    <h1 class="text-2xl font-bold mb-4">Editable Table</h1>
  
    {#if tableData.length > 0}
      <div class="relative overflow-x-auto shadow-md sm:rounded-lg">
        <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
          <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
            <tr>
              <th scope="col" class="px-6 py-3">ID</th>
              <th scope="col" class="px-6 py-3">Name</th>
              <th scope="col" class="px-6 py-3">Age</th>
            </tr>
          </thead>
          <tbody>
            {#each tableData as row, index}
              <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700">
                <td class="px-6 py-4">{row.id}</td>
                <td class="px-6 py-4">
                  <input
                    type="text"
                    class="w-full p-2 border border-gray-300 rounded-md"
                    value={row.name}
                    on:input={(e) => updateTableData(index, "name", e.target.value)}
                  />
                </td>
                <td class="px-6 py-4">
                  <input
                    type="number"
                    class="w-full p-2 border border-gray-300 rounded-md"
                    value={row.age}
                    on:input={(e) => updateTableData(index, "age", e.target.value)}
                  />
                </td>
              </tr>
            {/each}
          </tbody>
        </table>
      </div>
    {:else}
      <p>Loading data...</p>
    {/if}
  </div>
  