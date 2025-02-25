import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
from torch.utils.data import random_split

from pathlib import Path
import pandas as pd

from TracedDigitsDataset import TracedDigitsDataset
from OCR.OkraDigitCounter import OkraDigitCounter, TransposeImage, FlattenImage


CUDA_VISIBLE_DEVICES=1

# By default use the CPU
device = torch.device('cpu')

# Check for GPU
if torch.cuda.is_available():
    device = torch.device('cuda')
    # print('Using device:', torch.cuda.get_device_name(device))

else:
    print('Warning: No CUDA device available')


# Disable Debugging APIs (for better performance)
torch.autograd.set_detect_anomaly(mode=False)
torch.autograd.profiler.emit_nvtx(enabled=False)
torch.autograd.profiler.profile(enabled=False)


#############################
###### Hyperparameters ######

batch_size = 5
epochs = 100

lr = 0.0001
weight_decay = 1e-3

# SGD only
momentum = 0.97
nesterov = False

#############################
########## Options ##########

use_Adam_optimizer = False
load_existing_weights = False
input_weights_filename = 'okra-counter.pt'
output_final_weights_filename = 'okra-counter-final.pt'
output_best_weights_filename = 'okra-counter-best.pt'


# Transformations to be applied to the images
transform = transforms.Compose([
    transforms.ConvertImageDtype(torch.float32),
    transforms.Normalize(0.0, 1.0),
    FlattenImage(),
    TransposeImage()
])

#############################
#############################


def main():

    # Get data
    train_data, test_data = prepare_data()

    # Get model
    model = prepare_model()

    # Get optimizer
    optimizer = prepare_optimizer(model)

    # Get loss function
    criterion = nn.CrossEntropyLoss()

    # Run the training
    results = train_model(model, train_data, test_data, optimizer, criterion)

    # Save the final model
    torch.save(model.state_dict(), output_final_weights_filename)

    # Save the results
    results.to_csv('training results.csv')


######## Setup Functions ########

def prepare_data():

    data = TracedDigitsDataset(Path(__file__).parent / 'data' / 'TracedDigits', transform)

    train, test = random_split(data, [0.9, 0.1])

    train_loader = DataLoader(
        train,
        shuffle=True,
        batch_size=batch_size,
        num_workers=1,
        collate_fn=variable_size_collate
    )
    test_loader = DataLoader(test, shuffle=False, batch_size=1, num_workers=1)

    return train_loader, test_loader


def variable_size_collate(batch):
    data = [item[0] for item in batch]
    target = [item[1] for item in batch]
    target = torch.tensor(target)
    return [data, target]


def prepare_model():

    model = OkraDigitCounter()
    model.to(device)

    if load_existing_weights:

        state_dict = torch.load(
            Path(__file__).parent / input_weights_filename,
            weights_only=True,
            map_location=torch.device(device)
        )
        model.load_state_dict(state_dict)

    return model


def prepare_optimizer(model):

    if use_Adam_optimizer:

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=lr,
            weight_decay=weight_decay
        )

    else:

        optimizer = torch.optim.SGD(
            model.parameters(),
            lr=lr,
            momentum=momentum,
            nesterov=nesterov,
            weight_decay=weight_decay
        )

    return optimizer


######## Training/Testing Functions ########

def train_model(model, train_data, test_data, optimizer, criterion):

    results = pd.DataFrame(
        columns=['Testing Loss', 'Testing Accuracy', 'Training Loss', 'Training Accuracy']
    )

    best_accuracy = 0.0

    # Epoch 0 - Testing only
    #
    test_accuracy, test_loss = test(model, test_data, criterion)
    print(f'\nTesting:  accuracy = {test_accuracy:>0.2f}% | loss = {test_loss:.8f}')
    results.loc[0] = [test_loss, test_accuracy, '', '']

    try:
        for epoch in range(1, epochs + 1):

            print('\n------------ Epoch', epoch, '-----------')

            train_accuracy, train_loss = train_one_epoch(model, train_data, optimizer, criterion)
            print(f'Training: accuracy = {train_accuracy:>0.2f}% | loss = {train_loss:.8f}')

            test_accuracy, test_loss = test(model, test_data, criterion)
            print(f'Testing:  accuracy = {test_accuracy:>0.2f}% | loss = {test_loss:.8f}')

            # Save results
            results.loc[epoch] = [test_loss, test_accuracy, train_loss, train_accuracy]

            if epoch > 1 and test_accuracy > best_accuracy:
                best_accuracy = test_accuracy
                torch.save(model.state_dict(), output_best_weights_filename)

    except KeyboardInterrupt:
        print('KeyboardInterrupt: Saving results...')

    return results


def train_one_epoch(model, data, optimizer, criterion):

    # Set model to train mode
    model.train()

    total_correct = 0
    total_loss = 0

    for x_batch, labels in data:

        y_batch = get_one_hot_vectors(labels)

        # Erase old gradients by setting them to None
        optimizer.zero_grad(set_to_none=True)

        # Send data to GPU
        y_batch = y_batch.to(device)
        labels = labels.to(device)

        preds = None

        # Inference
        for x in x_batch:
            x = x.unsqueeze(dim=0)
            x = x.to(device)
            pred = model(x)
            pred = nn.functional.softmax(pred, dim=1)

            if preds is None:
                preds = pred
            else:
                preds = torch.cat((preds, pred), dim=0)

        # Calculate loss and update model parameters
        loss = criterion(preds, y_batch)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.25)
        optimizer.step()

        # Track statistics
        correct_pred = torch.argmax(preds, 1) == labels
        total_correct += correct_pred.float().sum().item()
        total_loss += loss.item()


    # Divide the loss from each batch by the number of batches
    avg_loss = total_loss / len(data)

    # Divide the number of correct predictions by the number of images
    accuracy = 100.0 * total_correct / len(data.dataset)

    return accuracy, avg_loss


def test(model, data, criterion):

    # Set model to test mode
    model.eval()

    total_correct = 0
    total_loss = 0

    with torch.no_grad():
        for x_batch, labels in data:

            y_batch = get_one_hot_vectors(labels)

            # Send data to GPU
            x_batch = x_batch.to(device)
            y_batch = y_batch.to(device)
            labels = labels.to(device)

            # Inference
            pred = model(x_batch)
            pred = nn.functional.softmax(pred, dim=1)

            # Compute loss for this batch
            total_loss += criterion(pred, y_batch).item()

            # Compute the number of correct predictions
            correct_pred = torch.argmax(pred, 1) == labels
            total_correct += correct_pred.float().sum().item()

    # Divide the loss from each batch by the number of batches
    avg_loss = total_loss / len(data)

    # Divide the number of correct predictions by the number of images
    accuracy = 100.0 * total_correct / len(data.dataset)

    return accuracy, avg_loss


def get_one_hot_vectors(labels):

    vectors = []

    for label in labels:
        v = [0] * 3
        v[label] = 1
        vectors.append(v)

    return torch.tensor(vectors, dtype=torch.float32)




if __name__=='__main__':
    main()
