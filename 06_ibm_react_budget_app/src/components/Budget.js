import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';

const Budget = () => {
    const context = useContext(AppContext);

    const upperLimit = 20000;

    const handleChange = (value) => {
        const numericValue = parseInt(value);
        if(numericValue > upperLimit) {
            alert("The value cannot exceed £" + upperLimit);
            return;
        }

        const totalExpenses = context.expenses.reduce((total, item) => {
            return (total += item.cost);
        }, 0);

        if(numericValue < totalExpenses) {
            alert("The budget can't be lower than the spending");
            return;
        }

        context.dispatch({
            type: 'SET_BUDGET',
            payload: value,
        });
    };

    return (
        <div className='alert alert-secondary'>
            <label htmlFor="budgetInput" style={{marginRight: '4px'}}>Budget: {context.currency}</label>
            <input
                required='required'
                type='number'
                id='budgetInput'
                value={context.budget}
                step="10"
                max={upperLimit}
                onChange={(event) => handleChange(event.target.value)}>
            </input>
        </div>
    );
};

export default Budget;