const BASE_URL = 'http://0.0.0.0:8000'

export const CREATE_TREE_ENDPOINT = BASE_URL + '/create/'
export const GET_TREE_ENDPOINT = BASE_URL + '/categories/'
export const UPDATE_TREE_ENDPOINT = BASE_URL + '/categories/update/'
export const DELETE_TREE_ENDPOINT = id => `${BASE_URL}/categories/delete/${id}/`
