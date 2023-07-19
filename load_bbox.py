from xml.dom.minidom import parse, parseString
import cv2
import glob
import json


def read_data(dataset_path, output_data):
   
  data=[]
  for filename_xml in glob.glob(dataset_path+'*.xml'):
    docs = parse(filename_xml)  # parse an XML file by name
    Coords = docs.getElementsByTagName("Coords")
    filename_img = (docs.getElementsByTagName("Page"))[0].getAttribute("imageFilename")
    count = 0
    bbox = []

    #print("%d Coords" % Coords.length)
    #print("")
    for i in Coords:

        #print("r" + str(count),":", i.getAttribute("points"))
        bbox.append(i.getAttribute("points"))
        count = count + 1

    #print("")

    Coords = docs.getElementsByTagName("Coords")
    count = 0
    types = []

    [types.append(item) for item in docs.getElementsByTagName("GraphicRegion")]
    [types.append(item) for item in docs.getElementsByTagName("TextRegion")]
    [types.append(item) for item in docs.getElementsByTagName("SeparatorRegion")]
      
    #types.append()
    list_types = [ele.getAttribute("id")  for ele in types]
    ordered_list = []
    ordered_list = sorted((item for item in types ), key=lambda x:int(x.getAttribute("id").replace('r', '')))
    #[print(ordered_list[index].tagName) for index in range(len(ordered_list))]
    #print(ordered_list[1].getAttribute("id"))
    #print("%d Types" % Coords.length)
    #print(len(ordered_list))
    bboxes = []

    for index, i in enumerate(Coords):
      split_inicial = docs.getElementsByTagName("Coords")[index].getAttribute("points").split()

      
      #print("id" + str(count),":", i.getAttribute("type"))
      #types.append(i.getAttribute("type"))
      #count = count + 1
      #print(index)
      class_bbox = ordered_list[index].tagName

      #for j in range(len(bbox)):
      #split_inicial = Coords[index]

      #print(split_inicial)
      split_final = []

      for j in range(len(split_inicial)):
        #print(split_inicial[i].split(','))
        split_final = split_final + split_inicial[j].split(',')

      #print(split_final)

      for k in range(len(split_final)):
        split_final[k] = int(split_final[k])

      #print(split_final)
      d = split_final

      Xs = d[::2]
      Ys = d[1::2]

      #print("")
      #print("X: ", Xs)
      #print("Y: ", Ys)

      #if len(Xs) == 4:
      #start_point = (min(Xs),min(Ys))
      #end_point = (max(Xs),max(Ys))

      bbox = [min(Xs),min(Ys), max(Xs), max(Ys)]

      bbox_obj = {
        'class': class_bbox,
        'bbox': bbox,
      }
      bboxes.append(bbox_obj)
    data_img = {'image': filename_img,
      'bboxes': bboxes
    }
    data.append(data_img)
  with open(output_data+"\\data.json", "w") as outfile:
    outfile.write(json.dumps(data))

if __name__== "__main__":
  from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
  import argparse
  

  parser = ArgumentParser(description="Load data to GBN dataset", formatter_class=ArgumentDefaultsHelpFormatter)


  parser.add_argument('--dataset', type=str, default='./', required=True,
                      help=('Directory to GBN dataset'))

  parser.add_argument('--output', type=str, default='./data.json', required=True,
                      help=('Directory to save json data'))

  args = parser.parse_args()
  print("Dataset: ", args.dataset)
  print("Output: ", args.output)

  read_data(args.dataset, args.output)


    #cv2.rectangle(img_copia, start_point, end_point, color=(255,0,0), thickness=4)

    #cv2.imshow('minha imagem',img_copia)
    #cv2.waitKey(0)


