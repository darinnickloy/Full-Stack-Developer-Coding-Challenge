import { ref } from 'vue'

const getAlerts = () => {

  const alerts = ref([])
  const error = ref(null)

  const load = async () => {
    try {
      let data = await fetch('https://nickloy-fullstack-challenge.herokuapp.com/api/alerts')
      if(!data.ok) {
        throw Error('no available data')
      }
      alerts.value = await data.json()
    }
    catch(err) {
      error.value = err.message
    }
  }

  return { alerts, error, load }
}

export default getAlerts