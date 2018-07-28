import { config } from '../config/config.jsx'

export function getURL(table){
  switch (table.value) {
    case 'Images':
      return config.url +'/images/upload'
    case 'Amazon Variations':
      return config.url + '/amazon/upload_variations'
    case 'Amazon Categories':
      return config.url + '/amazon/upload_category_report'
    default:
      return ''
  }
}