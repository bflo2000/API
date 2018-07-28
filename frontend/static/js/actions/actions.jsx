import axios from 'axios';
import { getURL } from '../utils/OperationUtils.jsx'

// navigation, for now
export const changeScreen = screen => ({
  type: 'CHANGE_SCREEN',
  screen
})

// placeholding screen names
export const screens = ({
  SCREEN1: 'SCREEN1',
  SCREEN2: 'SCREEN2',
  SCREEN3: 'SCREEN3'
})

// change RESTful request
export const changeRequest = request => ({
  type: 'CHANGE_REQUEST',
  request
})

export const updateFile = file => ({
  type: 'UPDATE_FILE',
  file
})

// Images and Amazon table, for now
export const tableSelect = table => ({
  type: 'SELECT_TABLE',
  table
})

// update the feedback viewport
export const updateFeedback = feedback => ({
  type: 'UPDATE_FEEDBACK',
  feedback
})

// just three for now
export const requests = ({
  POST: 'POST',
  PUT: 'PUT',
  DELETE: 'DELETE'
})

// Thunk returns a function, instead of an object

export function uploadCSV () {

  return (dispatch, getState) => {

  	// update state
    dispatch({type: 'IS_UPDATING'})

    // get request, file, and url from state tree
    let request_type = getState().apiRequest.request
    let file = getState().apiRequest.file
    let url = getURL(getState().apiRequest.table)
    // prepare form data
	let data = new FormData()
	data.append('csv_file', file[0])

	if(url){
	    switch (request_type){
			case 'POST':
	 			axios.post(url, data)
	 			.then(res => {
	 				if(res.status == 202){
						let message = res.data
						dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Ready', file: ''})
	        		}
	      		})
	      		.catch(error => {
	      			let message = error.response.data
	      			dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Loaded'})
	  			})
	      		break;  
			case 'DELETE':
				// axios does not accept a request body. Use config.data.
				axios.delete(url, {data: data})
				.then(res => {
	 				if(res.status == 202){
						let message = res.data
						dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Ready', file: ''})
	        		}
	      		})
	      		.catch(error => {
	      			let message = error.response.data
	      			dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Loaded'})
	  			}) 
				break
			case 'PUT':
				axios.put(url, data)
	 			.then(res => {
	 				if(res.status == 202){
						let message = res.data
						dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Ready', file: ''})
	        		}
	      		})
	      		.catch(error => {
	      			let message = error.response.data
	      			dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Loaded'})
	  			})
	      		break;  
		}
	}
	else{
		let message = "Please choose a table from the dropdown list."
		dispatch({type: 'UPDATE_FEEDBACK', feedback: message, status: 'Loaded'})
	}
  }
}