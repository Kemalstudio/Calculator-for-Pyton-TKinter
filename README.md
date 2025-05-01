Overall Purpose:

This Python code creates a graphical user interface (GUI) calculator application using the tkinter library (specifically using ttk for themed widgets). It functions like a standard desktop calculator but includes additional scientific functions in an expandable section.

Key Features and Functionality:

    GUI Structure:

        It creates a main window titled "Калькулятор" (Calculator).

        It uses the 'clam' theme from ttk for a slightly more modern visual style.

    Display Area:

        There's an Entry widget at the top that acts as the display. It shows the numbers and operators being entered (self.expression) and the final result of calculations.

        The display is set to 'readonly' most of the time, meaning the user cannot directly type into it; input comes from button clicks or keyboard bindings.

    Basic Buttons & Operations:

        It includes standard calculator buttons for digits (0-9), the decimal point (.), and basic arithmetic operators (+, -, *, /).

        It has buttons for:

            = (Equals): Evaluates the expression currently in the display.

            C (Clear): Clears the current expression in the display.

            Del (Delete): Removes the last character entered in the expression.

            ( and ): For handling parentheses in expressions.

    Expression Handling:

        As the user clicks buttons (or uses the keyboard), the corresponding characters are appended to an internal string variable self.expression.

        This self.expression string is continuously shown in the display Entry widget.

        When = is pressed, the code attempts to evaluate self.expression using Python's built-in eval() function. Note: While convenient, eval() can be a security risk if used with untrusted input, but it's common in simple calculator examples like this.

    Calculation History:

        A Listbox widget displays a history of completed calculations (e.g., "2+3 = 5").

        Every time a calculation is successfully completed with =, the full calculation (expression = result) is added to the self.history list and updated in the Listbox.

        A "Очистить историю" (Clear History) button appears when there's history available, allowing the user to clear both the Listbox and the internal self.history list.

    Clipboard Integration:

        "Копировать пример" (Copy Expression) button: Copies the current content of the display (which might be an ongoing expression or a final result) to the system clipboard.

        "Копировать ответ" (Copy Result - Note: The button text seems slightly misaligned with the code's function here. It copies the current expression string, not necessarily just the result after calculation): Copies the current expression string (self.expression) to the system clipboard.

    Extended/Scientific Mode:

        A "Развернуть" (Expand) / "Свернуть" (Collapse) button toggles the visibility of additional scientific function buttons.

        Extended Buttons: %, sin, cos, tan, √ (square root), π (pi), x² (square), x³ (cube).

        These buttons perform their respective mathematical operations (using Python's math module) on the value currently evaluated from the display. For trig functions (sin, cos, tan), it assumes the input is in degrees and converts it to radians before calculation.

        Activating this mode dynamically adjusts the window size to accommodate the new buttons.

    Keyboard Support:

        The calculator responds to keyboard input:

            Digits, operators (+, -, *, /), parentheses, decimal point.

            Enter key triggers the = calculation.

            Backspace key triggers the Del function.

            Escape key triggers the C (Clear) function.

        When a keyboard key corresponding to a button is pressed, the button on the GUI briefly highlights (appears pressed) for visual feedback.

    Error Handling:

        If the user enters an invalid expression (like "5++2") and presses =, the eval() function will raise an error.

        The code uses a try...except block to catch these errors. If an error occurs during calculation, the display shows "Ошибка" (Error), and the current expression is cleared.

In Summary:

The code builds a functional and interactive calculator with both basic and some advanced capabilities. It manages user input via buttons and keyboard, evaluates expressions, maintains a history, allows interaction with the clipboard, and provides visual feedback, all within a Tkinter GUI window.
