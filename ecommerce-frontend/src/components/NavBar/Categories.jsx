
const categoriesStyle = {
    display: "flex",
    width: "30%",
    gap: "12px"
}

export default function Categories({children}) {
    return (
        <div style={categoriesStyle}>
            {children}
        </div> 
    )
}