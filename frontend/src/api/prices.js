import axios from "axios";

BASE_URL = "http://localhost:8000/api";

export const fetchPrices = async () => {
    const response = await axios.get(`${BASE_URL}/prices`)
    return response.data.prices;
}