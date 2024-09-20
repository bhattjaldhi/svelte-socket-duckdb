import { writable } from 'svelte/store';
import io from 'socket.io-client';

const SERVER_URL = process.env.VITE_SERVER_URL || 'http://localhost:5000';

function createTableStore() {
    const tableData = writable([]);
    /**
     * @type {import("socket.io-client").Socket<import("@socket.io/component-emitter").DefaultEventsMap, import("@socket.io/component-emitter").DefaultEventsMap> | null}
     */
    let socket;

    return {
        subscribe: tableData.subscribe,
        initSocket: () => {
            try {
                socket = io(SERVER_URL);
                
                socket.on('connect', () => {
                    console.log('Connected to server');
                });

                socket.on('connect_error', (error) => {
                    console.error('Connection error:', error);
                });

                socket.on('update_success', (data) => {
                    console.log(`Update successful for row: ${data.row_id}, column: ${data.column}`);
                });

                socket.on('cell_update_broadcast', (data) => {
                    const { row_id, column, new_value } = data;
                    tableData.update(value => {
                        let _tableData = [...value]
                        _tableData[row_id][column] = new_value
                        return [..._tableData];
                    });
                });

                socket.on('update_failure', (data) => {
                    console.error('Update failed:', data);
                });
            } catch (error) {
                console.error('Error initializing socket:', error);
            }
        },
        fetchData: async () => {
            try {
                const response = await fetch(`${SERVER_URL}/api/table`);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                tableData.set(data);
            } catch (error) {
                console.error("Error fetching data:", error);
            }
        },
        updateCell: (rowId, column, value) => {
            if (socket && socket.connected) {
                socket.emit('cell_update', { row_id: rowId, column: column, new_value: value });
                tableData.update(value => {
                    let _tableData = [...value]
                    _tableData[rowId][column] = value
                    return [..._tableData];
                });
            } else {
                console.error('Socket not connected. Unable to update cell.');
            }
        },
        destroySocket: () => {
            if (socket) {
                socket.disconnect();
                socket = null;
            }
        }
    };
}

export const tableStore = createTableStore();