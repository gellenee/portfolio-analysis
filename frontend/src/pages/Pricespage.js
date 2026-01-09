import {usePrices} from "../hooks/usePrices"
import {Table} from "../components/Table"

export const Pricespage = () => {
    const {prices, error, isLoading} = usePrices()

    // define columns of the table
    const columns = [
        {"key": "date", "label":"Date"}, 
        {"key": "symbol", "label":"Symbol"},
        {"key": "close_price", "label":"Close Price"}, 
    ]

    if (isLoading) return <p>Loading...</p>
    if (error) return <p>Error: {error}</p>

    return (
        <div>
            {console.log(prices)}
            <h1>Portfolio prices </h1>
            <Table columns = {columns} data = {prices}/>
            
        </div>
    )
}