import Categories from "./Categories"
import SearchBar from "./SearchBar"
import DropDown from "./DropDown"
import AnchorLink from "./AnchorLink"
import OptionWindow from "./OptionWindow"
import UserSettings from "./UserSettings"
import { useState } from "react"

import { HiShoppingBag } from "react-icons/hi2";

const navBarStyle = {
    width: "100%",
    display: "flex",
    gap: "3px",
    borderRadius: "3px",
    padding: "24px 12px",
    boxShadow: "0px 0px 6px 0px rgba(0,0,0,0.5)",
    backgroundColor: 'whitesmoke',
    alignItems: "center",
    fontFamily: "sans-serif"
}

const logoStyle = {
    width: "5%"
}



export default function NavBar() {

    const [categoryDropdownOpen, setCategoryDropdownOpen]  = useState(false);
    const [accountDropdownOpen, setAccountDropdownOpen] = useState(false);


    return (
        <nav style={navBarStyle}>
            <span style={logoStyle}> <HiShoppingBag size={24}/> </span>
            <Categories>
                <AnchorLink linkName="Electronics"/>
                <AnchorLink linkName="Books"/>
                <AnchorLink linkName="Clothing"/>
                <AnchorLink linkName="Home & Kitchen"/>
                <DropDown setState={setCategoryDropdownOpen} isOpen={categoryDropdownOpen}>
                    <OptionWindow width="80px">
                        <AnchorLink linkName="Sports"/>
                        <AnchorLink linkName="Toys"/>
                        <AnchorLink linkName="Beauty"/>
                        <AnchorLink linkName="Baby"/>
                    </OptionWindow>
                </DropDown>
            </Categories>   
            <SearchBar/>
            <UserSettings>
                <DropDown setState={setAccountDropdownOpen} text="User" isOpen={accountDropdownOpen} >
                    <OptionWindow>
                        <AnchorLink linkName="My Account"/>
                        <AnchorLink linkName="Shopping Cart"/>
                        <AnchorLink linkName="Orders"/>
                        <AnchorLink linkName="Logout"/>
                    </OptionWindow>
                </DropDown>
            </UserSettings>
        </nav>
    )
}



