import axios from 'axios';

export const changeScreen = screen => ({
  type: 'CHANGE_SCREEN',
  screen
})

export const screens = ({
  SCREEN1: 'SCREEN1',
  SCREEN2: 'SCREEN2',
  SCREEN3: 'SCREEN3'
})

export const changeRequest = request => ({
  type: 'CHANGE_REQUEST',
  request
})

export const updateFile = file => ({
  type: 'UPDATE_FILE',
  file
})

export const requests = ({
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE'
})

export function uploadCSV (file) {
  updateFile(file)
  return (dispatch, getState) => {
    dispatch({type: 'IS_UPDATING'});
    switch (getState().apiRequest.request){
		case 'POST':
 			axios.post('http://192.168.99.100:8000/images/upload', file).then(res => 
 			{
        		console.log(res);
        		console.log(res.data);
      		})  
		case 'DELETE':
			axios.delete('http://192.168.99.100:8000/images/upload', file) 
		case 'PUT':
			axios.put('http://192.168.99.100:8000/images/upload', file)
	}
    /*.then((res) =>{
        dispatch({type: CREATE_ORGANIZATION_SUCCESS, payload: res});
    })
    .catch((error)=> {
        dispatch({type: CREATE_ORGANIZATION_FAILURE, payload: error});
    })*/
  }
}