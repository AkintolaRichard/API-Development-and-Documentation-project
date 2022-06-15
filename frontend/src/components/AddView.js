import React from 'react';
import FormView from './FormView';
import FormViewCategory from './CategoryFormView';

function AddView() {
    return (
      <div>
          <FormViewCategory/>
          <FormView/>
      </div>
    );
  }
   
  export default AddView;