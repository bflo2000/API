import { config } from '../config/config.jsx'

export function getURL(table){
  switch (table.value) {
    case 'Images':
      return config.url +'/images/upload'
    case 'Amazon':
      return config.url + '/amazon/upload_variations'
    default:
      return ''
  }
}