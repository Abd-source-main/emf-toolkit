import sympy as sp
from flask import flash


class CalcIntegral:
    @staticmethod
    def _integrate_step(current_expression, var_char, lower_str, upper_str):
        var_symbol = sp.symbols(var_char)
        lower_limit = sp.sympify(lower_str)
        upper_limit = sp.sympify(upper_str)
        return sp.integrate(current_expression, (var_symbol, lower_limit, upper_limit))

    @classmethod
    def integrate_function(cls, expression_str, variable_limits):
        if not expression_str or not variable_limits:
            flash("Please fill in all fields.", "error")
            return None

        try:
            current_expression = sp.sympify(expression_str)

            # Loop through variables (Inner -> Outer)
            for var_char, lower_str, upper_str in variable_limits:
                current_expression = cls._integrate_step(
                    current_expression,
                    var_char,
                    lower_str,
                    upper_str
                )

            # Final Evaluation
            sympy_result = current_expression.evalf()
            if str(sympy_result).isdigit():
                final_result = round(float(sympy_result), 10)  # type: ignore
            else:
                # maybe keep it as an object if have problems
                final_result = str(sympy_result)
            return final_result

        except Exception as e:

            print(e)
            # flash(f"Calculation Error: {str(e)}", "error")
            return None


class CalcChargeFromLamdas:
    @staticmethod
    def _prepare_limits(vars_input, lowers_input, uppers_input):
        """
        Helper: Ensures inputs are always lists, then zips them into tuples.:
          - lamda_l(..., "x", "0", "1")
          - lamda_s(..., ["x", "y"], ["0", "0"], ["1", "1"])
        """
        # If inputs are single strings, wrap them in a list
        if not isinstance(vars_input, list):
            vars_input = [vars_input]
        if not isinstance(lowers_input, list):
            lowers_input = [lowers_input]
        if not isinstance(uppers_input, list):
            uppers_input = [uppers_input]

        #  Zip them into the format: [('x', '0', '1'), ('y', '0', 'x')]
        return list(zip(vars_input, lowers_input, uppers_input))

    @staticmethod
    def lamda_l(expression, var_char, lower_limit, upper_limit):
        limits = CalcChargeFromLamdas._prepare_limits(
            var_char, lower_limit, upper_limit)

        return CalcIntegral.integrate_function(expression, limits)

    @staticmethod
    def lamda_s(expression, var_chars, lower_limits, upper_limits):
        limits = CalcChargeFromLamdas._prepare_limits(
            var_chars, lower_limits, upper_limits)

        return CalcIntegral.integrate_function(expression, limits)

    @staticmethod
    def lamda_v(expression, var_chars, lower_limits, upper_limits):
        limits = CalcChargeFromLamdas._prepare_limits(
            var_chars, lower_limits, upper_limits)

        return CalcIntegral.integrate_function(expression, limits)


if __name__ == "__main__":

    result = CalcChargeFromLamdas.lamda_v(
        '(1/(x**3 * y**3 * z**3))* 10**-6', ["x", 'y', 'z'], ['0.1', '0.1', '0.1'], ['1', '2', '2'])
    print(result)
