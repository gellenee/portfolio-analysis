// reusable table component 
export const Table = ({columns, data}) => {
    return (
        <table>
            <thead>
                <tr>
                    {columns.map((col) => (
                        <th key ={col.key}> {col.label}</th>
                    ))}
                </tr>
            </thead>

            <tbody>
                {data.map((row) => (
                    <tr key = {row.date_id + row.asset_id}>
                        {columns.map((col) => (
                            <td key = {col.key}>{row[col.key]}</td>
                        ))}
                    </tr>
                ))}
            </tbody>

        </table>
    )
}