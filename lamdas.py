import sympy as sp
from flask import flash


class CalcIntegral:
    @staticmethod
    def integrate_function(expression_str, variable_limits):
        if not expression_str or not variable_limits:
            flash("Please fill in all fields.", "error")
            return None

        try:
            local_context = {'e': sp.E, 'pi': sp.pi, 'exp': sp.exp}

            # Use locals dictionary to enforce correct interpretation
            current_expression = sp.sympify(
                expression_str, locals=local_context)

            # Loop through variables (Inner -> Outer)
            for var_char, lower_str, upper_str in variable_limits:
                current_expression = Preparers._integrate_step(
                    current_expression,
                    var_char,
                    lower_str,
                    upper_str
                )

            # Final Evaluation
            sympy_result = current_expression.evalf()

            # Convert to string
            final_result = str(sympy_result)
            return final_result

        except Exception as e:
            print(f"Integration Error: {e}")
            # flash(f"Calculation Error: {str(e)}", "error")
            return f"Error: {str(e)}"


class Preparers():
    @staticmethod
    def _integrate_step(current_expression, var_char, lower_str, upper_str):
        # Define context for limits to understand 'e' and 'pi'
        local_context = {'e': sp.E, 'pi': sp.pi, 'exp': sp.exp}

        var_symbol = sp.symbols(var_char)
        lower_limit = sp.sympify(lower_str, locals=local_context)
        upper_limit = sp.sympify(upper_str, locals=local_context)

        return sp.integrate(current_expression, (var_symbol, lower_limit, upper_limit))

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


class CalcChargeFromLamdas(Preparers):

    @classmethod
    def lamda_l(cls, expression, var_char, lower_limit, upper_limit):
        limits = cls._prepare_limits(
            var_char, lower_limit, upper_limit)

        return CalcIntegral.integrate_function(expression, limits)

    @classmethod
    def lamda_s(cls, expression, var_chars, lower_limits, upper_limits):
        limits = cls._prepare_limits(
            var_chars, lower_limits, upper_limits)

        return CalcIntegral.integrate_function(expression, limits)

    @classmethod
    def lamda_v(cls, expression, var_chars, lower_limits, upper_limits):
        limits = cls._prepare_limits(
            var_chars, lower_limits, upper_limits)

        return CalcIntegral.integrate_function(expression, limits)

    @classmethod
    def calculate_total_charge(cls, density_expr, coords, h_factors, active_vars, active_lowers, active_uppers, fixed_subs):
        """
        Logic to combine density, h-factors, and fixed variable substitution
        before integrating.
        """
        # 1. Handle Substitutions for Fixed Variables
        # Create copies to avoid modifying originals
        current_h_factors = list(h_factors)
        current_density = density_expr

        for var_name, val_str in fixed_subs.items():
            # Replace in h_factors (e.g. : replace 'r' in 'r*sin(theta)' as r is constant)
            for k in range(len(current_h_factors)):
                current_h_factors[k] = current_h_factors[k].replace(
                    var_name, val_str)

            # Replace in density expression
            current_density = current_density.replace(var_name, val_str)

        # 2. Construct Final Integrand
        # Integrand = Density * Product(h_factors of ACTIVE vars)
        final_h_factors = []
        for i in range(len(coords)):
            var_name = coords[i]
            if var_name in active_vars:
                # Only include the active h factor
                # and it is not '1'
                if current_h_factors[i] != '1':
                    final_h_factors.append(current_h_factors[i])

        final_expr_str = current_density
        if final_h_factors:
            # format the list to string for injection
            jacobian_mult = "*".join(final_h_factors)
            final_expr_str = f"({current_density}) * {jacobian_mult}"

        # 3. Call Specific Lambda Function based on number of active variables
        num_vars = len(active_vars)

        if num_vars == 1:
            return cls.lamda_l(final_expr_str, active_vars[0], active_lowers[0], active_uppers[0])
        elif num_vars == 2:
            return cls.lamda_s(final_expr_str, active_vars, active_lowers, active_uppers)
        elif num_vars == 3:
            return cls.lamda_v(final_expr_str, active_vars, active_lowers, active_uppers)
        else:
            return "Error: No dimensions selected for integration."


if __name__ == "__main__":
    result = CalcChargeFromLamdas.lamda_v(
        '(e**x)', ["x"], ['0'], ['1'])
    print(f"{result}")
