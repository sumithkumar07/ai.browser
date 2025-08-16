// Fix for React boolean attribute warnings
// This utility ensures boolean props are handled correctly

export const safeBoolean = (value) => {
  if (value === true) return true;
  if (value === false) return false;
  return undefined; // Don't pass the prop at all if it's not a boolean
};

export const safeBooleanProps = (props) => {
  const cleaned = {};
  Object.keys(props).forEach(key => {
    const value = props[key];
    if (typeof value === 'boolean') {
      cleaned[key] = value;
    } else if (value !== null && value !== undefined) {
      cleaned[key] = value;
    }
  });
  return cleaned;
};

// Common boolean attributes that cause warnings
export const cleanDOMProps = (props) => {
  const {
    // Remove React-only props that shouldn't be passed to DOM
    key,
    ref,
    children,
    dangerouslySetInnerHTML,
    // Remove custom props that might cause issues
    isActive,
    isSelected,
    isDisabled,
    isVisible,
    showLabel,
    ...domProps
  } = props;

  // Convert boolean-like strings to actual booleans
  Object.keys(domProps).forEach(key => {
    const value = domProps[key];
    if (value === 'true') domProps[key] = true;
    if (value === 'false') domProps[key] = false;
    if (value === '') delete domProps[key];
  });

  return domProps;
};