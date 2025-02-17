import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';

const Remaining = () => {
    const context = useContext(AppContext);
    const totalExpenses = context.expenses.reduce((total, item) => {
        return (total = total + item.cost);
    }, 0);
    const alertType = totalExpenses > context.budget ? 'alert-danger' : 'alert-success';
    return (
        <div className={`alert ${alertType}`}>
            <span>Remaining: {context.currency}{context.budget - totalExpenses}</span>
        </div>
    );
};

export default Remaining