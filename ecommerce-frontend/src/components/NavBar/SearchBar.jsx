import { FaSearch } from "react-icons/fa";

const searchBarStyle = {
    display: "flex",
    flexDirection: "row",
    width: "35%",
    columnGap: "12px",
    alignItems: "center"
}

const inputStyle = {
    border: "none",
    outline: "none",
    width: "80%",
    color: "#686D76",
    height: "48px",
    padding: "0px 12px",
}

const logoStyle = {
    cursor: 'pointer',
}

export default function SearchBar() {
    return (
        <div style={searchBarStyle}>
            <input style={inputStyle} type="text" value="" placeholder="What are you searching for?"/>
            <span style={logoStyle}><FaSearch size={24}/></span>
        </div>
    )
}