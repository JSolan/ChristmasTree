# Christmas tree lights

## WLED LED Control with Python

This project is a Python application to control a WLED-powered LED strip or matrix. It allows you to apply effects, reset segments, and interact dynamically with the LEDs via the WLED JSON API.

---

## Hardware

Currently a [dig2go](https://dig2go.info/) 5v WLED controller plugged into a string of 100 rgb LEDs. (https://www.amazon.co.uk/BTF-LIGHTING-Decorative-Addressable-Christmas-Controller/dp/B08LKPF2PX). No affliation to either link. This is currently a cheap and cheerful setup to test the idea before likley going to 12V and something with a bit more oomph. 

## Features
- Apply built-in WLED effects (e.g., Rainbow, Twinkle, Fireworks).
- Interactive terminal input for dynamic control of effects, palettes, and LED counts.
- See https://kno.wled.ge/ for more features of WLED

---

## Usage

1. **Install requirements**, detailed in requirements.txt
```
pip install -r requirements.txt
```

2. **Run the Application**
   - Start the main script:
     ```bash
     python main.py
     ```

3. **Follow Prompts**
   - Enter the **Effect ID** (e.g., `9` for Rainbow).
   - Enter the **Palette ID** (default is `0`).
   - Enter the **Total Number of LEDs** in your strip or matrix.

---

## Contributing
Feel free to open issues or pull requests to improve the project! Contributions are always welcome.

---

## License
This project is licensed under the MIT License.