import Categories from "./Categories"
import SearchBar from "./SearchBar"
import DropDown from "./DropDown"
import AnchorLink from "./AnchorLink"
import OptionWindow from "./OptionWindow"
import UserSettings from "./UserSettings"
import { useState } from "react"
const navBarStyle = {
    width: "100%",
    display: "flex",
    gap: "3px",
    border: "1px solid black",
    borderRadius: "3px"
}

const logoStyle = {
    width: "10%"
}



export default function NavBar() {

    const [categoryDropdownOpen, setCategoryDropdownOpen]  = useState(false);
    const [accountDropdownOpen, setAccountDropdownOpen] = useState(false);


    return (
        <nav style={navBarStyle}>
            <span style={logoStyle}> x </span>
            <Categories>
                <AnchorLink/>
                <AnchorLink/>
                <AnchorLink/>
                <AnchorLink/>
                <AnchorLink/>
                <DropDown setState={setCategoryDropdownOpen} isOpen={categoryDropdownOpen}>
                    <OptionWindow>
                        <AnchorLink/>
                        <AnchorLink/>
                        <AnchorLink/>
                        <AnchorLink/>
                    </OptionWindow>
                </DropDown>
            </Categories>   
            <SearchBar/>
            <UserSettings>
                <DropDown setState={setAccountDropdownOpen} text="Account..." isOpen={accountDropdownOpen} >
                    <OptionWindow>
                        <AnchorLink/>
                        <AnchorLink/>
                        <AnchorLink/>
                        <AnchorLink/>
                    </OptionWindow>
                </DropDown>
            </UserSettings>
        </nav>
    )
}



