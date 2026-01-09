import { useEffect, useState } from "react"
import {fetchPrices} from "../api/prices"

export const usePrices = () => {
    const [prices, setPrices] = useState([]);
    const [error, setError] = useState(null)
    const [isLoading, setLoading] = useState(true)

    // dependency array empty means will only run on first render
    useEffect(() => {
        const getData = async() => {
            try{
                // cant use await in this scope so have to wrap an async function inside
                const data = await fetchPrices();
                setPrices(data)
            } catch (err){
                setError(err.message);
            } finally{
                setLoading(false);
            }
        };
        getData()
    }, []); 
    return {prices, error, isLoading}
}