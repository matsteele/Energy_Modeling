import merge from 'lodash/merge';
import ISWRITING from '../actions/writingState-actions';


const isWritingReducer = (state='notWriting', action) =>{
  Object.freeze(state);
  switch(action.type){
    case "ISWRITING":
      const writingState = action.payload;
      return writingState
    default:
      return state;
  }
};


export default isWritingReducer;
