export const date_string_to_float = (date_string) => {
    let without_letters = date_string.replaceAll("-", "").replaceAll("T", "").replaceAll(":", "").replaceAll("Z", "");
    return parseFloat(without_letters);
};