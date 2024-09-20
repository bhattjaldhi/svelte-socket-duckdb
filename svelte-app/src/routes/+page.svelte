<script>
   import { onMount, onDestroy } from "svelte";
  import { tableStore } from '../store/tableStore';

  let tableData = [];

  // Subscribe to the tableStore
  const unsubscribe = tableStore.subscribe(value => {
    tableData = value;
  });

  onMount(() => {
    tableStore.initSocket();
    tableStore.fetchData();
  });

  onDestroy(() => {
    // Close the socket connection when the component is destroyed
    tableStore.destroySocket();
    // Unsubscribe from the store
    unsubscribe();
  });

  // Update the tableData and send the change to the server
  const updateTableData = (rowId, field, value) => {
    tableStore.updateCell(rowId, field, value);
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
  