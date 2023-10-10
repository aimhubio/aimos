import { Text } from 'components/kit_v2';

function TextVizElement(props: any) {
  return (
    <Text {...props.options} as={props.options.component || 'p'}>
      {props.data}
    </Text>
  );
}

export default TextVizElement;
