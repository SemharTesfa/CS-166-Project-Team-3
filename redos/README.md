## Recommendations:
* Ensure regexes are as strict as possible and try to avoid nested quantifiers or operations prone to branching and backtracking.  
    - Regexes branching operations can te be tested and visualized with programs such [regex101](https://regex101.com/)
* Consider using a state machine parser such as Ragel for complex regexes
* Rate limit routes with regexes that can be potentially computationally expensive
* Whenever possible use pre defined regexes in common use such as phone/email
* Whenever possible avoid exposing regexes directly to user input
* Use client side form validation whenever possible to avoid computationally costly operations on the server side to minimize the damage of bad regexes
* If a regex needs to be exposed to user input, escape special characters
* Configure your server to timeout requests and kill threads that take too long