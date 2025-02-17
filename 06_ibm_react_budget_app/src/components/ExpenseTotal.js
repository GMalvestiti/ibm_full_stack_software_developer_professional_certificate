import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';

const ExpenseTotal = () => {
    const context = useContext(AppContext);
    const totalExpenses = context.expenses.reduce((total, item) => {
        return (total += item.cost);
    }, 0);
    return (
        <div className='alert alert-primary'>
            <span>Spent so far: {context.currency}{totalExpenses}</span>
        </div>
    );
};

export default ExpenseTotal;