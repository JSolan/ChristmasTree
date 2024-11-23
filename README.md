# Christmas tree lights

## WLED LED Control with Python

This project is a Python application to control a WLED-powered LED strip or matrix. It allows you to apply effects, reset segments, and interact dynamically with the LEDs via the WLED JSON API.

---

## Features
- Apply built-in WLED effects (e.g., Rainbow, Twinkle, Fireworks).
- Reset segment configurations and unfreeze LEDs (`frz: false`).
- Interactive terminal input for dynamic control of effects, palettes, and LED counts.
- Modular design for scalability and maintainability.

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

## Contributing
Feel free to open issues or pull requests to improve the project! Contributions are always welcome.

---

## License
This project is licensed under the MIT License.