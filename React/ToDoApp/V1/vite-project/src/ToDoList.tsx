import React, { useState } from 'react'

interface item {
    id: number;
    text: string;
    completed: boolean;
}


export const ToDoList: React.FC = () => {
    const [todos, setTodos] = useState<item[]>([{id: 1, text: "Test", completed:false}]);
    const [input, setInput] = useState<string>("")

    const handleToggle = (id: number) => {
        setTodos(
            todos.map((todo) => {
                if (todo.id === id) {
                    return { ...todo, completed: !todo.completed };
                }
                return todo;
            })
        );
    };

    const handleClick = () => {
        let newId = 1;
        while (todos.some(items => items.id === newId)) {
            newId = newId + 1
        }
        console.log(newId)
        const newTodo: item = {id: newId, text:input, completed:false}
        setTodos([...todos, newTodo]);
    }

    return <div className='main-container'>
        <h1>To Do List</h1>
        <ul>
            {todos.map((todo) => (
                <li key={todo.id} onClick={() => handleToggle(todo.id)} style={{ textDecoration: todo.completed ? "line-through" : "none" }} >{todo.text}</li>
            ))}
        </ul>
        <input  
            type='text'
            placeholder='Add todo item'
            onChange={(e) => setInput(e.currentTarget.value)}
        />
        <button onClick={handleClick}>Add</button>
    </div>
}
