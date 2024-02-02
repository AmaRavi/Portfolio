import React, { useState } from 'react'

interface item {
    id: number;
    text: string;
    completed: boolean;
}

interface orderList {
    priority: number[]
}


export const ToDoList: React.FC = () => {
    const [todos, setTodos] = useState<item[]>([]);
    const [input, setInput] = useState<string>("")
    const [options, setOptions] = useState<number[]>;
    

    const handleToggle = (id: number) => {

        // Create new array with item deleted
        const updatedArray = todos.filter((item) => item.id !== id);

        // Update each item id with index + 1
        const updatedArrayWithUpdatedIds = updatedArray.map((item, index) => ({
            ...item,
            id: index + 1,
        }));

        // Update new array
        setTodos(updatedArrayWithUpdatedIds);
    };

    const handleClick = () => {
        let newId = 1;
        while (todos.some(items => items.id === newId)) {
            newId = newId + 1
        }
        const newTodo: item = {id: newId, text:input, completed:false}
        setTodos([...todos, newTodo]);
    }

    const getOptionsList = () => {
        const arrayList = [...Array(todos.length)].map((_, index) => index + 1);
        return arrayList
    }

    return <div className='main-container'>
        <h1>To Do List</h1>
        <ul>
            <ol>
                {todos.map((todo) => (
                    <li key={todo.id} onClick={() => handleToggle(todo.id)} >{todo.text}</li>
                ))}
            </ol>
        </ul>
        <input  
            type='text'
            placeholder='Add todo item'
            onChange={(e) => setInput(e.currentTarget.value)}
        />
        <></>
        <button onClick={handleClick}>Add</button>
    </div>
}
