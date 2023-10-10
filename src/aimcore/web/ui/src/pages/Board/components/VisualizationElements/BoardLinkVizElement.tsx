import * as React from 'react';

import { IconLayout2, IconExternalLink } from '@tabler/icons-react';

import { Link, Button, Text } from 'components/kit_v2';

import { PathEnum } from 'config/enums/routesEnum';

import useApp from 'pages/Apps/useApp';

function BoardLinkVizElement(props: any) {
  const { data: boardsList, appName } = useApp();

  const url = new URL(window.location.href);

  const isEditMode =
    url.pathname.startsWith(PathEnum.Apps) && url.pathname.endsWith('/edit');

  const packageName = props.options.package_name;
  const stateParam = props.options.state_param;

  let externalPackageNameLastIndex = props.data.indexOf(':');

  let externalPackage =
    externalPackageNameLastIndex === -1
      ? null
      : props.data.slice(0, externalPackageNameLastIndex);

  const boardPath = externalPackage
    ? props.data
    : packageName && !boardsList.includes(props.data)
    ? `${packageName}:${props.data}`
    : props.data;

  return (
    <Link
      css={{
        display: 'flex',
        color: '$textPrimary',
        textDecoration: 'underline',
        textDecorationColor: '$textPrimary50',
      }}
      to={`${PathEnum.App.replace(':appName', appName as string)}/${boardPath}${
        isEditMode ? '/edit' : ''
      }${stateParam ? '?state=' + stateParam : ''}`}
      target={props.options.new_tab ? '_blank' : undefined}
    >
      <Button
        leftIcon={<IconLayout2 color='#45484D' />}
        rightIcon={
          props.options.new_tab && <IconExternalLink color='#45484D' />
        }
        horizontalSpacing='compact'
        size='md'
        variant='ghost'
        color='secondary'
      >
        <Text>{props.options.text}</Text>
      </Button>
    </Link>
  );
}
export default BoardLinkVizElement;
