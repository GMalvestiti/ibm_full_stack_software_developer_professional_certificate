import React, { useContext } from 'react';
import { TiDelete } from 'react-icons/ti';
import { BiSolidPlusCircle, BiSolidMinusCircle } from "react-icons/bi";
import { AppContext } from '../context/AppContext';

const ExpenseItem = (props) => {
    const context = useContext(AppContext);

    const handleDeleteExpense = () => {
        context.dispatch({
            type: 'DELETE_EXPENSE',
            payload: props.id,
        });
    };

    const increaseAllocation = (name) => {
        const expense = {
            name: name,
            cost: 10,
        };

        context.dispatch({
            type: 'ADD_EXPENSE',
            payload: expense
        });
    }

    const decreaseAllocation = (name) => {
        const expense = {
            name: name,
            cost: 10,
        };

        context.dispatch({
            type: 'RED_EXPENSE',
            payload: expense
        });
    }

    return (
        <tr>
        <td>{props.name}</td>
        <td>{context.currency}{props.cost}</td>
        <td><BiSolidPlusCircle style={{color: "#63b863"}} size='2em' onClick={event=> increaseAllocation(props.name)}></BiSolidPlusCircle></td>
        <td><BiSolidMinusCircle style={{color: "red"}} size='2em' onClick={event=> decreaseAllocation(props.name)}></BiSolidMinusCircle></td>
        <td><TiDelete size='1.5em' onClick={handleDeleteExpense}></TiDelete></td>
        </tr>
    );
};

export default ExpenseItem;