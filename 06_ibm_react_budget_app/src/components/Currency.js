import React, { useContext } from 'react';
import { AppContext } from '../context/AppContext';
import './Currency.css';

const Currency = () => {
    const context = useContext(AppContext);

    const changeCurrency = (value)=>{
        context.dispatch({
            type: 'CHG_CURRENCY',
            payload: value,
        })
    };
    
    return (
        <div className='alert alert-secondary style-div'> Currency
            <select className='style-select' name="Currency"  id="Currency" onChange={event=>changeCurrency(event.target.value)}>
                <option value="$" className='select-option'>Dollar ($)</option>
                <option value="£" className='select-option' selected>Pound (£)</option>
                <option value="€" className='select-option'>Euro (€)</option>
                <option value="₹" className='select-option'>Rupee (₹)</option>
            </select>
        </div>
    );
};

export default Currency;