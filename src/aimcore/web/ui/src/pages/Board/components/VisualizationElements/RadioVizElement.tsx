import * as React from 'react';

import { Radio, RadioGroup, Text } from 'components/kit_v2';
import { RadioLabel } from 'components/kit_v2/Radio/Radio.style';

function RadioVizElement(props: any) {
  const [value, setValue] = React.useState<string>(`${props.options.value}`);

  const onChange = React.useCallback(
    (value: string) => {
      setValue(value);
      props.callbacks?.on_change(value);
    },
    // eslint-disable-next-line react-hooks/exhaustive-deps
    [],
  );

  const options = React.useMemo(
    () => props.options.options.map((option: string) => `${option}`),
    [props.options.options],
  );

  React.useEffect(() => {
    if (props.options.value !== value) {
      setValue(`${props.options.value}`);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [props.options.value]);

  const id = React.useMemo(() => `radio_${Date.now()}`, []);
  return (
    <div>
      {props.options.label && (
        <Text as='label' htmlFor={id} disabled={props.options.disabled}>
          {props.options.label}
        </Text>
      )}
      <RadioGroup
        id={id}
        orientation={props.options.orientation}
        onValueChange={onChange}
        value={value}
        disabled={props.options.disabled}
      >
        {options.map((option: string) => (
          <Radio key={option} value={option}>
            <Text>{option}</Text>
          </Radio>
        ))}
      </RadioGroup>
    </div>
  );
}
export default RadioVizElement;
